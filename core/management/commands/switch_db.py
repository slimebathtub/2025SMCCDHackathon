# myapp/management/commands/switch_db.py
import sys
import os
import shutil
import tempfile
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
from dotenv import dotenv_values

class Command(BaseCommand):
    help = (
        "Switch between local and production databases, check current DB,"
        " or pull production data into local without duplicating system tables."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=[
                'local',         # copy .env.local → .env
                'prod',          # copy .env.production → .env
                'check',         # print current DATABASES['default']
                'copy_from_prod' # pull production DB data into local
            ],
            help=(
                "'local': switch to .env.local; "
                "'prod': switch to .env.production; "
                "'check': show current DB; "
                "'copy_from_prod': when on local, dump prod data (excluding system tables) and load into local"
            )
        )

    def handle(self, *args, **options):
        action = options['action']
        project_root = settings.BASE_DIR
        env_local = os.path.join(project_root, '.env.local')
        env_prod = os.path.join(project_root, '.env.production')
        env_file = os.path.join(project_root, '.env')

        def _copy(src, dst, desc):
            if not os.path.exists(src):
                raise CommandError(f"Env file not found: {src}")
            shutil.copyfile(src, dst)
            self.stdout.write(self.style.SUCCESS(f"✅ {desc}"))

        if action in ('local', 'prod'):
            src = env_local if action == 'local' else env_prod
            _copy(src, env_file, f"Switched .env to {os.path.basename(src)}")

        elif action == 'check':
            default_db = settings.DATABASES.get('default', {})
            host = default_db.get('HOST', '')
            if host:
                self.stdout.write(self.style.SUCCESS(f"→ Using PRODUCTION DB (HOST='{host}')"))
            else:
                self.stdout.write(self.style.SUCCESS("→ Using LOCAL SQLite DB"))

        elif action == 'copy_from_prod':
            # Ensure current DB is local
            current_host = settings.DATABASES.get('default', {}).get('HOST', '')
            if current_host:
                raise CommandError("copy_from_prod can only be run when connected to LOCAL database")

            # 1) Switch to production env for dump
            _copy(env_prod, env_file, "Temporarily switched .env to .env.production for dump")

            # 2) Prepare environment variables from .env.production
            prod_env = dotenv_values(env_prod)
            proc_env = os.environ.copy()
            proc_env.update({k: v for k, v in prod_env.items() if v is not None})

            # 3) Dump production data via subprocess
            fd, dump_path = tempfile.mkstemp(prefix='prod_data_', suffix='.json')
            os.close(fd)
            try:
                dump_cmd = [
                    sys.executable,
                    os.path.join(project_root, 'manage.py'),
                    'dumpdata',
                    '--exclude', 'contenttypes',
                    '--exclude', 'auth.Permission',
                    '--exclude', 'admin.LogEntry',
                    '--indent', '2',
                    f'--output={dump_path}'
                ]
                self.stdout.write(f"Running: {' '.join(dump_cmd)}")
                subprocess.run(dump_cmd, check=True, cwd=project_root, env=proc_env)
                self.stdout.write(self.style.SUCCESS(f"✅ Dumped production data to {dump_path}"))

                # 4) Restore local env
                _copy(env_local, env_file, "Restored .env from .env.local")

                # 5) Flush and migrate local DB
                call_command('flush', '--no-input')
                call_command('migrate')
                self.stdout.write(self.style.SUCCESS("✅ Local DB flushed and migrated"))

                # 6) Load dumped production data into local DB via subprocess
                load_cmd = [
                    sys.executable,
                    os.path.join(project_root, 'manage.py'),
                    'loaddata',
                    dump_path
                ]
                self.stdout.write(f"Running: {' '.join(load_cmd)}")
                subprocess.run(load_cmd, check=True, cwd=project_root)
                self.stdout.write(self.style.SUCCESS("✅ Production data loaded into local DB"))

            finally:
                if os.path.exists(dump_path):
                    os.remove(dump_path)
                    self.stdout.write(self.style.SUCCESS(f"Removed temporary dump file {dump_path}"))

        else:
            raise CommandError(f"Unknown action: {action}")

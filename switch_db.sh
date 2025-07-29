#!/bin/bash

if [ "$1" == "prod" ]; then
    cp .env.production .env
    echo "✅ Switched to Cloud PostgreSQL"
elif [ "$1" == "local" ]; then
    cp .env.local .env
    echo "✅ Switched to Local SQLite"
else
    echo "❌ Usage: ./switch_db.sh [local|prod]"
fi

# for windows users

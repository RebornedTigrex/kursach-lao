## Развёртывание через Docker

```bash
# Сборка и запуск всего стека
docker-compose up --build
# После этого фронт доступен на http://localhost:3000, backend — на http://localhost:8000
```

## CI/CD

- Все pull request и коммиты в ветки main, master, develop автоматически проверяются GitHub Actions.
- Запускаются линтер и тесты (pytest).
- Workflow-файл: `.github/workflows/ci.yml`
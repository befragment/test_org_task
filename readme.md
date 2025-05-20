## Job test case 

### In order to launch use: 

```bash
docker compose up -d 
docker compose exec backend bash 
python scripts/genmock.py  # if mock data is needed 
uvicorn main:app --host 0.0.0.0 --port 8000
```

After launching the app, go to: `http://127.0.0.1:8000/docs` for Swagger Documentation
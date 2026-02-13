@echo off
echo ========================================
echo Langflow + Langfuse Diagnostic Script
echo ========================================
echo.

echo [1/8] Checking if Langfuse is running...
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose ps | findstr langfuse
echo.

echo [2/8] Checking if Langflow is running...
cd c:\Users\tamil\repo\tamilsmtp\dockers\langflow
docker compose ps | findstr langflow
echo.

echo [3/8] Checking Langfuse environment variables in Langflow...
docker compose exec -T langflow env | findstr LANGFUSE
echo.

echo [4/8] Checking Langflow environment variables...
docker compose exec -T langflow env | findstr LANGFLOW_LANGFUSE
echo.

echo [5/8] Testing connectivity from Langflow to Langfuse...
docker compose exec -T langflow curl -s -o NUL -w "HTTP Status: %%{http_code}\n" http://host.docker.internal:3000/api/public/health
echo.

echo [6/8] Checking recent Langflow logs for Langfuse mentions...
docker compose logs langflow --tail 50 | findstr /i langfuse
echo.

echo [7/8] Checking for any errors in Langflow...
docker compose logs langflow --tail 50 | findstr /i "error fail exception"
echo.

echo [8/8] Checking Langfuse logs for incoming requests...
cd c:\Users\tamil\repo\tamilsmtp\dockers\langfuse
docker compose logs langfuse --tail 30 | findstr /i "trace api"
echo.

echo ========================================
echo Diagnostic Complete!
echo ========================================
echo.
echo Next steps:
echo 1. If Langfuse is not running: cd langfuse && docker compose up -d
echo 2. If Langflow is not running: cd langflow && docker compose up -d
echo 3. If connectivity fails: Check if Langfuse is accessible at http://localhost:3000
echo 4. If no Langfuse env vars: Restart Langflow with docker compose restart langflow
echo.
pause

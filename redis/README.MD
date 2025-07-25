
To secure Redis with a password, you can pass the `requirepass` argument in the `command` section of your `docker-compose.yml` file.

The best practice is to use an environment file (`.env`) to store the password instead of hardcoding it.

-----

### \#\# 1. Create a `.env` File 🤫

First, create a file named `.env` in the same directory as your `docker-compose.yml` file. This file will securely store your password.

**.env**

```
REDIS_PASSWORD=your-super-secret-password
```

**Note**: Replace `your-super-secret-password` with a strong, unique password.

-----

### \#\# 2. Update the `docker-compose.yml` File 🔒

Now, modify your `docker-compose.yml` to use this password.

**docker-compose.yml**

```yaml
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: my-secure-redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes

volumes:
  redis-data:
```

#### **Explanation of Changes**

  * **`command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes`**: We've added the `--requirepass` flag. `docker-compose` automatically replaces `${REDIS_PASSWORD}` with the value from your `.env` file when it starts the container.

-----

### \#\# 3. How to Use 🚀

1.  Make sure both the `.env` and `docker-compose.yml` files are in the same directory.
2.  Start the container:
    ```bash
    docker-compose up -d
    ```
3.  Connect to your Redis instance. You will now need to authenticate.
    ```bash
    docker exec -it my-secure-redis redis-cli
    ```
4.  Once inside the Redis CLI, use the `AUTH` command with your password:
    ```
    127.0.0.1:6379> AUTH your-super-secret-password
    OK
    ```
5.  You can now run commands as usual:
    ```
    127.0.0.1:6379> ping
    PONG
    ```
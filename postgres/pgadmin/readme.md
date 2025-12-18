sudo systemctl restart postgresql

sudo apt update
sudo apt install -y postgresql-16 postgresql-server-dev-16

cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector


make
sudo make install
sudo -u postgres psql

CREATE DATABASE vectordb;
\c vectordb
CREATE EXTENSION vector;

\dx


CREATE TABLE embeddings (
  id bigserial PRIMARY KEY,
  embedding vector(3)
);

INSERT INTO embeddings (embedding)
VALUES ('[0.1, 0.2, 0.3]');

SELECT * FROM embeddings;


CREATE INDEX ON embeddings
USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);


CREATE INDEX ON embeddings
USING hnsw (embedding vector_l2_ops);

sudo nano /etc/postgresql/16/main/postgresql.conf

shared_buffers = 2GB
work_mem = 64MB
maintenance_work_mem = 512MB
effective_cache_size = 6GB

sudo systemctl restart postgresql


> ❌ `vector.control` not found
> ✅ PostgreSQL is installed
> ❌ **pgvector is NOT installed on the system**

```
/usr/share/postgresql/16/extension/vector.control
```

That file is created **only when pgvector is installed against PostgreSQL 16**.

Common causes:

* pgvector was never installed
* pgvector built for PG 15, but you’re running PG 16
* `postgresql-server-dev-16` was missing during build

---

# ✅ Correct Fix (Step-by-step)

## 1️⃣ Confirm PostgreSQL version

```bash
psql --version
pg_config --version
```

You should see **PostgreSQL 16.x** in both.

If `pg_config` points to another version, tell me — that matters.

---

## 2️⃣ Ensure PG dev headers are installed (required)

```bash
sudo apt install -y postgresql-server-dev-16 build-essential git
```

Verify:

```bash
ls /usr/lib/postgresql/16/include
```

---

## 3️⃣ Install pgvector **from source (recommended)**

```bash
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
```

Build:

```bash
make
```

Install:

```bash
sudo make install
```

---

## 4️⃣ Verify pgvector files exist

```bash
ls /usr/share/postgresql/16/extension | grep vector
```

You **must** see:

```
vector.control
vector--*.sql
```

Also check:

```bash
ls /usr/lib/postgresql/16/lib | grep vector
```

Expected:

```
vector.so
```

---

## 5️⃣ Restart PostgreSQL

```bash
sudo systemctl restart postgresql
```

---

## 6️⃣ Create extension (this will now work)

```bash
sudo -u postgres psql vectordb
```

```sql
CREATE EXTENSION vector;
```

Verify:

```sql
\dx
```

Expected:

```
vector | 0.5.x | vector data type and similarity search
```

---

# ✅ If you prefer a faster way (package-based)

If DNS + apt are stable **now**, you can install pgvector via package:

```bash
sudo apt install -y postgresql-16-pgvector
```

Then:

```bash
sudo systemctl restart postgresql
```

> But source install is more reliable in restricted networks (which you clearly have).

---

# 🧪 Quick sanity test

```sql
CREATE TABLE test_vec (
  id serial,
  embedding vector(3)
);

INSERT INTO test_vec VALUES (1, '[0.1,0.2,0.3]');

SELECT embedding <=> '[0.1,0.2,0.4]' FROM test_vec;
```

---

# 🔐 About your GRANT command

This part is **already correct**:

```sql
GRANT ALL PRIVILEGES ON DATABASE vectordb TO vector_user;
```

Once `CREATE EXTENSION vector` succeeds, your `vector_user` can fully use it.

---

# 🚨 If it STILL fails, send me this output

```bash
pg_config --pkglibdir
pg_config --sharedir
ls -ld /usr/share/postgresql/*
```

Below are **safe, correct steps to expose PostgreSQL port 5432 on Ubuntu to your local (home) network** — **not the internet**.
## ⚠️ Security note (important)

Exposing PostgreSQL is **fine on a home LAN**, but:

* ❌ Do NOT expose to `0.0.0.0/0` without firewall rules
* ✅ Restrict to **LAN subnet**
* ✅ Use **password auth**
* ✅ Prefer **non-postgres user**

---

# ✅ Step-by-step

---

## 1️⃣ Find your Ubuntu machine’s LAN IP

```bash
ip a | grep inet
```

Example:

```
inet 192.168.1.50/24
```

👉 We’ll assume subnet: `192.168.1.0/24`

---

## 2️⃣ Configure PostgreSQL to listen on network

Edit:

```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

Change:

```conf
#listen_addresses = 'localhost'
```

To:

```conf
listen_addresses = 'localhost,192.168.1.50'
```

Or (simpler for LAN):

```conf
listen_addresses = '*'
```

Save & exit.

---

## 3️⃣ Allow LAN access in pg_hba.conf

Edit:

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Add **below existing rules**:

```conf
# Allow home network
host    all    all    192.168.1.0/24    md5
```

👉 Replace subnet if needed (`10.0.0.0/24`, etc.)

---

## 4️⃣ Restart PostgreSQL

```bash
sudo systemctl restart postgresql
```

Verify listening:

```bash
ss -lntp | grep 5432
```

Expected:

```
LISTEN 0 244 0.0.0.0:5432
```

---

## 5️⃣ Open firewall (UFW) for local network only

Check if UFW is enabled:

```bash
sudo ufw status
```

If enabled, allow LAN:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw reload
```

Verify:

```bash
sudo ufw status
```

You should see:

```
5432 ALLOW 192.168.1.0/24
```

---

That message means PostgreSQL is reachable on **192.168.10.17:5432**, but it’s **rejecting the client (192.168.10.18)** because `pg_hba.conf` doesn’t have a matching rule for that **host + user + db**, for **either SSL or non-SSL**.

Fix = add the right `pg_hba.conf` entries for your LAN subnet.

---

## 1) Add a pg_hba rule for your home subnet

On **192.168.10.17** (the DB server), edit:

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Add these lines **near the top of the “IPv4 local connections” section** (order matters):

```conf
# Allow vector_user from home LAN to vectordb (non-SSL)
host    vectordb    vector_user    192.168.10.0/24    scram-sha-256

# Allow vector_user from home LAN to vectordb (SSL)
hostssl vectordb    vector_user    192.168.10.0/24    scram-sha-256
```

> If you don’t want SSL right now, you can omit the `hostssl` line, but leaving it is fine.

---

## 2) Ensure the user has a password (SCRAM is recommended)

```bash
sudo -u postgres psql
```

Run:

```sql
ALTER ROLE vector_user WITH PASSWORD 'StrongPwd@123';
```

(Optional, but good) ensure scram is used:

```sql
SHOW password_encryption;
```

If it’s not `scram-sha-256`, set it (in `postgresql.conf`):

```conf
password_encryption = scram-sha-256
```

Then restart.

---

## 3) Reload PostgreSQL (or restart)

Reload is enough for `pg_hba.conf` changes:

```bash
sudo systemctl reload postgresql
```

If you changed `postgresql.conf`, do restart:

```bash
sudo systemctl restart postgresql
```

---

## 4) Test again from the client (192.168.10.18)

### Non-SSL test:

```bash
psql "host=192.168.10.17 port=5432 dbname=vectordb user=vector_user sslmode=disable"
```

### SSL preferred (works with self-signed too):

```bash
psql "host=192.168.10.17 port=5432 dbname=vectordb user=vector_user sslmode=prefer"
```

---

## 5) If it STILL fails: check which rules PostgreSQL is reading

On server:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
sudo -u postgres psql -c "SELECT pg_reload_conf();"
```

And show the effective rules area:

```bash
sudo grep -n "192.168.10" /etc/postgresql/16/main/pg_hba.conf
```


sudo -u postgres psql

CREATE USER vector_user WITH PASSWORD 'Welcome123';
CREATE DATABASE vectordb OWNER vector_user;
\c vectordb
CREATE EXTENSION vector;

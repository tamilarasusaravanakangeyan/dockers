pgvector-learn

```
import csv
from pathlib import Path

import numpy as np
import psycopg
from pgvector.psycopg import register_vector

DSN = "host=localhost port=6024 dbname=vectordb user=vector password=vector"
DATA = Path.cwd().parent / "data"  # Jupyter notebooks do not define __file__

conn = psycopg.connect(DSN, autocommit=True)
print("connected; pgvector extension ready\n")
```

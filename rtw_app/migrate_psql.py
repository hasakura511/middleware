import os
import sys
print(sys.argv)
desc = ' '.join(sys.argv[1:])
os.system(f'alembic revision --autogenerate -m "{desc}"')
os.system('alembic upgrade head')

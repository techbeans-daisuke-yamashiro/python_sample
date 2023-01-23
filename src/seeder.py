#database seeder

from database import create_db_and_tables, create_seed_data

def main():
    create_db_and_tables()
    create_seed_data()

if __name__ == '__main__':
    main()

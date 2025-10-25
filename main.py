from app import extractor, transformer, db_loader


def main():
    db_loader.create_table()

    raw_data = extractor.fetch_data()
    transformed = transformer.process_data(raw_data)
    if transformed is not None:
        db_loader.load_to_db(transformed)
        print(transformed.head())
    else:
        print("Data processing failed")


if __name__ == "__main__":
    main()

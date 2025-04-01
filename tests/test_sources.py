from app import db, Source, create_app

app = create_app()

with app.app_context():
    # Add a new source
    new_source = Source(link="https://example.com", source_type="Article")
    db.session.add(new_source)
    db.session.commit()

    # Fetch and print all sources
    sources = Source.query.all()
    for src in sources:
        print(f"Source: {src.link}, Type: {src.source_type}")

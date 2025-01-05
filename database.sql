CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    author VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (name, version)
);

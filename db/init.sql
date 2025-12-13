CREATE TABLE IF NOT EXISTS documents (
    id_cr VARCHAR(10) PRIMARY KEY NOT NULL UNIQUE,
    title VARCHAR(400) NOT NULL,
    MCB VARCHAR(400),
    age_category VARCHAR(20) NOT NULL,
    developer VARCHAR(1000),
    placement_date DATE,
    data BYTEA NOT NULL,
    creator VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            login VARCHAR(255) UNIQUE NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'admin')),
            created_at TIMESTAMP DEFAULT NOW()
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE table_name = 'documents'
          AND constraint_name = 'chk_documents_age'
    ) THEN
        ALTER TABLE documents
        ADD CONSTRAINT chk_documents_age CHECK (
            age_category IN ('Взрослые', 'Дети', 'Взрослые, дети')
        );
    END IF;
END
$$;
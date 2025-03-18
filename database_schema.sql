CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL,
    image_path TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE wood_entries (
    id SERIAL PRIMARY KEY,
    log_id INT REFERENCES logs(id) ON DELETE CASCADE,
    wood_type VARCHAR(50) NOT NULL,
    length_cm INT NOT NULL,
    diameter_cm INT NOT NULL,
    quantity INT NOT NULL,
    volume_m3 FLOAT NOT NULL
);

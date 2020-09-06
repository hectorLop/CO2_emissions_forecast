CREATE TABLE registry (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	registered_date TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
	model TEXT NOT NULL,
	parameters TEXT NOT NULL,
	metrics TEXT NOT NULL,
	remote_path TEXT NOT NULL,
	training_time REAL NOT NULL,
	dataset TEXT NOT NULL
);
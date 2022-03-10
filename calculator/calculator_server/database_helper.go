package main

import (
	"database/sql"
	"log"
	"os"
)

func createAndConnectToSQLiteDB() (*sql.DB, error) {
	// remove db file if already excist.
	os.Remove("sqlite_part_database.db")

	log.Println("Creating sqlite_part_database.db...")
	// Create SQLite file
	file, err := os.Create("sqlite_part_database.db")
	if err != nil {
		return nil, err
	}
	file.Close()
	log.Println("sqlite_part_database.db file created")

	// Open the created SQLite File
	sqliteDatabase, err := sql.Open("sqlite3", "./sqlite_part_database.db")
	if err != nil {
		return nil, err
	}
	// Create Database Tables
	err = createTable(sqliteDatabase)
	if err != nil {
		return nil, err
	}

	return sqliteDatabase, nil
}

func createTable(db *sql.DB) error {
	// SQL Statement for Create Table
	createPartTableSQL := `
	CREATE TABLE factory_parts
						(id TEXT PRIMARY KEY, 
						title TEXT)`

	log.Println("Create student table...")
	statement, err := db.Prepare(createPartTableSQL) // Prepare SQL Statement
	if err != nil {
		return err
	}

	// Execute SQL Statements
	_, err = statement.Exec()
	if err != nil {
		return err
	}
	log.Println("part table created")
	return nil
}

func insertPart(db *sql.DB, id string, title string, image string) {
	log.Println("Inserting student record ...")
	insertPartSQL := `INSERT INTO student(id, title, image) VALUES (?, ?, ?)`
	statement, err := db.Prepare(insertPartSQL) // Prepare statement.
	// This is good to avoid SQL injections
	if err != nil {
		log.Fatalln(err.Error())
	}
	_, err = statement.Exec(id, title, image)
	if err != nil {
		log.Fatalln(err.Error())
	}
}

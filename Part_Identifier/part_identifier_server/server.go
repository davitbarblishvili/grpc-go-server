package main

import (
	"context"
	"database/sql"
	"fmt"
	"grpc_go/greetings/Part_Identifier/PartIdentifierpb"
	"log"
	"net"
	"os"

	_ "github.com/mattn/go-sqlite3"
	"google.golang.org/grpc"
)

type server struct {
	PartIdentifierpb.UnimplementedPartIdentifierServiceServer
	db *sql.DB
}

func (s *server) IdentifyPart(ctx context.Context, req *PartIdentifierpb.IdentifyPartRequest) (*PartIdentifierpb.IdentifyPartResponse, error) {
	fmt.Printf("Received Part Identification Request: %v\n", req)

	res, err := getPartFromDB(s.db, req.GetPartId())

	if err != nil {
		return nil, err
	}

	return res, nil
}

func main() {

	fmt.Println("Part Identifier Server")

	db, err := createAndConnectToSQLiteDB()

	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	insertPart(db, "0001", "Intermediate Shaft",
		"https://i5.walmartimages.com/asr/dbb29ded-aea1-4bd2-865b-2392d43026f0.a1c57c0a22f983cc7e399327ae9b4081.png?odnHeight=612&odnWidth=612&odnBg=FFFFFF",
		"68167997AB", "main_storage")

	lis, err := net.Listen("tcp", ":4054")

	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	PartIdentifierpb.RegisterPartIdentifierServiceServer(s, &server{db: db})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}

}

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
						title TEXT, 
						image TEXT, 
						part_number TEXT, 
						location TEXT)`

	log.Println("Create factory_parts table...")
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

func insertPart(db *sql.DB, id string, title string, image string, part_number string, location string) {
	log.Println("Inserting part record ...")
	insertPartSQL := `INSERT INTO factory_parts(id, title, image, part_number, location) VALUES (?, ?, ?, ?, ?)`
	statement, err := db.Prepare(insertPartSQL) // Prepare statement.
	// This is good to avoid SQL injections
	if err != nil {
		log.Fatalln(err.Error())
	}
	_, err = statement.Exec(id, title, image, part_number, location)
	if err != nil {
		log.Fatalln(err.Error())
	}
}

func getPartFromDB(db *sql.DB, id string) (*PartIdentifierpb.IdentifyPartResponse, error) {
	log.Println("Invoked getPartFromDB Function ...")

	row, err := db.Query("select * from factory_parts where id = $1;", id)
	if err != nil {
		return nil, err
	}
	defer row.Close()

	resp := new(PartIdentifierpb.IdentifyPartResponse)

	for row.Next() {
		// Iterate and fetch the records from result cursor
		err := row.Scan(&resp.Id, &resp.Title, &resp.ImageUrl, &resp.PartNumber, &resp.Location)
		if err != nil {
			return nil, err
		}
	}
	return resp, nil
}

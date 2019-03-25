BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "energylevel" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"isotopologue_id"	TEXT,
	"exomol_ID"	INTEGER,
	"energy"	INTEGER,
	"degeneracy" REAL,
	"J"	REAL,
	"Tparity"	TEXT,
	"Rparity"	TEXT,
	"state"	TEXT,
	"v"	INTEGER,
	"Lambda"	INTEGER,
	"Sigma"	INTEGER,
	"Omega"	INTEGER,
	FOREIGN KEY("isotopologue_id") REFERENCES "Isotopologue"("id")
);
CREATE TABLE IF NOT EXISTS "transition" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"isotopologue_id"	INTEGER,
	"exomol_ID"	TEXT,
	"upper_id"	INTEGER,
	"lower_id"	INTEGER,
	"einstien_A"	REAL,
	"intensity"	REAL,
	"wavenumber"	REAL,
	"change_mu"		REAL,
	"change_nu"		REAL,
	"change_I"		REAL,
	"K_mu"	REAL, 
	"K_I"	REAL,
	FOREIGN KEY("isotopologue_id") REFERENCES "Isotopologue"("id"),
	FOREIGN KEY("upper_id") REFERENCES "energylevel"("id"),
	FOREIGN KEY("lower_id") REFERENCES "energylevel"("id")
);
CREATE TABLE IF NOT EXISTS "isotopologue" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	INTEGER NOT NULL,
	"temperature"	INTEGER NOT NULL,
	"g_ns"	INTEGER NOT NULL,
	"Q_T"	REAL
);
COMMIT;

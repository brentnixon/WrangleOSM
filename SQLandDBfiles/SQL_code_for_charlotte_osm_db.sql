
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

.mode csv
.import nodes.csv nodes
.import ways.csv ways
.import nodes_tags.csv nodes_tags
.import ways_nodes.csv ways_nodes
.import ways_tags.csv ways_tags

DELETE FROM nodes where id = 'id';
DELETE FROM ways where id = 'id';
DELETE FROM nodes_tags where id = 'id';
DELETE FROM ways_nodes where id = 'id';
DELETE FROM ways_tags where id = 'id';

.mode columns
.header on

CREATE VIEW UserContributionTotals AS
SELECT COUNT(waysnnodes.uid) as UserTotals, waysnnodes.user
FROM (
    SELECT nodes.uid, nodes.user 
    FROM nodes 
    UNION ALL 
    SELECT ways.uid, ways.user 
    FROM ways) waysnnodes
GROUP BY waysnnodes.uid
ORDER BY COUNT(waysnnodes.uid) DESC
;

CREATE VIEW nodeANDway_tags AS
        SELECT *
        FROM nodes_tags
            UNION ALL 
        SELECT *
        FROM ways_tags
;
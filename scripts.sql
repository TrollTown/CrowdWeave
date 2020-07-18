-- Create places table
CREATE TABLE places (
place_id TEXT NOT NULL,
popular_times_response TEXT);

-- Create ratings table
CREATE TABLE ratings (
place_id TEXT NOT NULL,
rating INTEGER);
Django OMDb Api Project for Postman Task

1) Movie details endpoint - '/api/movie/?title=Inception'
  Takes a movie title as a query parameter.
  Fetches data from OMDb using t=<title>.
  Cleans up the response to only include key info like Title, Year, Plot, Country, Director, etc.
  Returns an easy-to-read JSON payload.
  Purpose: Quickly get clean, structured movie details.

2) Episode details endpoint - '/api/episode/?Title=Friends&Season=1&Epnumber=2'
  Takes series title, season, and episode number.
  Uses OMDb’s episode query (t, Season, and Episode) to get specific episode info.
  Returns structured JSON with title, director, actors, plot, IMDb rating, etc.
  Purpose: Fetch info for specific TV show episodes.

3) Genre Search - '/api/genre/?genre=Action'
  OMDb doesn’t let you directly search by genre — so this dictionary maps each genre name to related keywords.
  Reads the genre parameter (e.g., "Action").
  Uses related keywords to perform multiple OMDb searches.
  Fetches detailed movie info for each result.
  Filters out only movies that actually match the requested genre.
  Sorts them by IMDb rating.
  Returns Top 15 movies.
  Purpose: To help your genre-based search system find movies more intelligently.

4) Recommendation - '/api/recommendations/?favmovie=Interstellar'
  Fetches details for the favorite movie.
  Extracts its Genre, Director, and Actors.
  Runs a three-level recommendation algorithm:
    level1 : genre (Highest)
    level2 : director 
    level3 : actors (Lowest)
  Each level searches OMDb, fetches movie details, filters relevant results, and sorts by IMDb rating.
  Combines all results and returns the top 20 best-rated recommendations.
  Purpose: Smart, layered movie recommendation system using existing metadata.
  
5) Health Check - '/api/health/'
  Just confirms your API server is up and running.
  Purpose: Useful for testing or deployment monitoring tools

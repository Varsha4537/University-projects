#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Movie
{
public:
    string title;
    float vote_average;
    int vote_count;
    string status;
    string release_date;
    long long revenue;
    int runtime;
    bool adult;
    long long budget;
    string original_language;
    string original_title;
    string overview;
    float popularity;
    string tagline;
    vector<string> genres;
    vector<string> production_companies;
    vector<string> production_countries;
    vector<string> spoken_languages;
};

// Function to remove double quotes from the start and end of a string
string removeQuotes(const string &str)
{
    string cleaned_str = str;

    // Remove leading and trailing quotes if present
    if (!cleaned_str.empty())
    {
        if (cleaned_str.front() == '"' && cleaned_str.back() == '"')
        {
            cleaned_str = cleaned_str.substr(1, cleaned_str.size() - 2);
        }
    }

    return cleaned_str;
}

// Function to split a string by a delimiter and return tokens as vector
vector<string> split_strings(const string &line, char delimiter, const vector<bool> &remove_quotes)
{
    vector<string> tokens;
    stringstream ss(line);
    string token;
    size_t index = 0;
    bool in_quotes = false; // Flag to track if currently inside quoted text
    while (getline(ss, token, delimiter))
    {
        // Check if removal of quotes is required for this token
        if (!remove_quotes.empty() && index < remove_quotes.size() && remove_quotes[index])
        {
            token = removeQuotes(token);
        }

        // If inside quoted text, continue reading until ending quote is found
        while (token.front() == '"' && !in_quotes)
        {
            // Check if token ends with double quote
            if (token.back() == '"')
            {
                // Remove double quotes from token
                token.erase(token.begin());
                token.pop_back();
                break;
            }
            else
            {
                // Read next token and append to current token
                string next_token;
                if (!getline(ss, next_token, delimiter))
                {
                    cerr << "Error: Ending quote not found for token: " << token << endl;
                    break;
                }
                token += delimiter + next_token;
            }
        }

        // Check if current token starts a quoted text
        if (token.front() == '"' && !in_quotes)
        {
            in_quotes = true;
        }

        // Check if current token ends the quoted text
        if (token.back() == '"' && in_quotes)
        {
            in_quotes = false;
        }

        tokens.push_back(token);
        index++;
    }
    return tokens;
}

// Function to split a string by a delimiter and return non-empty tokens as vector
vector<string> split(const string &line, char delimiter)
{
    vector<string> tokens;
    stringstream ss(line);
    string token;
    while (getline(ss, token, delimiter))
    {
        if (!token.empty())
        {
            tokens.push_back(token);
        }
    }
    return tokens;
}

// Function to parse CSV file and populate vector of Movie objects
vector<Movie> parseCSV(const string &filename, vector<bool> &remove_quotes)
{
    vector<Movie> movies;

    ifstream file(filename);
    if (!file.is_open())
    {
        cerr << "Error opening file: " << filename << endl;
        return movies;
    }

    string line;
    // Skip header line
    getline(file, line);
    while (getline(file, line))
    {
        Movie movie;
        vector<string> tokens = split_strings(line, ',', remove_quotes);

        // Fill movie struct with tokens
        movie.title = tokens[1];
        movie.vote_average = stof(tokens[2]);
        movie.vote_count = stoi(tokens[3]);
        movie.status = tokens[4];
        movie.release_date = tokens[5];
        movie.revenue = stoll(tokens[6]);
        movie.runtime = stoi(tokens[7]);
        movie.adult = (tokens[8] == "False" || tokens[8] == "0");
        movie.budget = stoll(tokens[10]);
        movie.original_language = tokens[13];
        movie.original_title = tokens[14];
        if (!tokens[15].empty())
            movie.overview = tokens[15];
        if (!tokens[16].empty())
        {
            movie.popularity = stof(tokens[16]);
        }
        if (!tokens[18].empty())
            movie.tagline = tokens[18];

        // Parse genres
        vector<string> genres = split(tokens[19], '|');
        movie.genres = move(genres);

        // Parse production companies
        vector<string> production_companies = split(tokens[20], '|');
        if (!tokens[20].empty())
            movie.production_companies = move(production_companies);

        // Parse production countries
        vector<string> production_countries = split(tokens[21], '|');
        if (!tokens[21].empty())
            movie.production_countries = move(production_countries);

        // Parse spoken languages
        vector<string> spoken_languages = split(tokens[22], '|');
        if (!tokens[22].empty())
            movie.spoken_languages = move(spoken_languages);

        movies.push_back(move(movie));
    }

    file.close();

    return movies;
}

// Function to merge two sorted vectors of movies based on popularity
vector<Movie> merge(vector<Movie>& left, vector<Movie>& right) {
    vector<Movie> merged;
    int i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i].popularity >= right[j].popularity) {
            merged.push_back(left[i]);
            i++;
        } else {
            merged.push_back(right[j]);
            j++;
        }
    }
    while (i < left.size()) {
        merged.push_back(left[i]);
        i++;
    }
    while (j < right.size()) {
        merged.push_back(right[j]);
        j++;
    }
    return merged;
}

// Function to perform merge sort on vector of movies based on popularity
vector<Movie> mergeSort(vector<Movie>& movies) {
    if (movies.size() <= 1) {
        return movies;
    }
    int mid = movies.size() / 2;
    vector<Movie> left(movies.begin(), movies.begin() + mid);
    vector<Movie> right(movies.begin() + mid, movies.end());
    left = mergeSort(left);
    right = mergeSort(right);
    return merge(left, right);
}

void languageDistribution(const vector<Movie>& movies) {
    vector<string> languages;
    vector<int> languageCount;
    
    // Iterate through the movies to count language frequency
    for (const auto& movie : movies) {
        bool languageFound = false;
        for (size_t i = 0; i < languages.size(); ++i) {
            if (movie.original_language == languages[i]) {
                languageCount[i]++;
                languageFound = true;
                break;
            }
        }
        if (!languageFound) {
            languages.push_back(movie.original_language);
            languageCount.push_back(1);
        }
    }
    
    // Display language distribution
    cout << "Language Distribution:" << endl;
    for (size_t i = 0; i < languages.size(); ++i) {
        cout << languages[i] << ": " << languageCount[i] << " movies" << endl;
    }}
    
    void analyzeRuntimeDistribution(const vector<int>& runtimes) {
        // Create a copy of the runtimes vector to avoid modifying the original data
        vector<int> sortedRuntimes = runtimes;

        // Perform merge sort on the copy
        mergeSort(sortedRuntimes, 0, sortedRuntimes.size() - 1);

        // Calculate mean, median, mode, and standard deviation using the sorted data
        double mean = 0;
        for (int runtime : sortedRuntimes) {
            mean += runtime;
        }
        mean /= sortedRuntimes.size();

        int median = sortedRuntimes[sortedRuntimes.size() / 2];

        int mode = 0, modeCount = 0;
        for (int i = 0; i < sortedRuntimes.size(); ++i) {
            int count = 1;
            while (i + 1 < sortedRuntimes.size() && sortedRuntimes[i] == sortedRuntimes[i + 1]) {
                ++count;
                ++i;
            }
            if (count > modeCount) {
                modeCount = count;
                mode = sortedRuntimes[i];
            }
        }

        double sumSquaredDifferences = 0;
        for (int runtime : sortedRuntimes) {
            double difference = runtime - mean;
            sumSquaredDifferences += difference * difference;
        }
        double variance = sumSquaredDifferences / sortedRuntimes.size();
        double stdDeviation = sqrt(variance);

        // Print the computed statistics
        cout << "Mean Runtime: " << mean << endl;
        cout << "Median Runtime: " << median << endl;
        cout << "Mode Runtime: " << mode << " (appeared " << modeCount << " times)" << endl;
        cout << "Standard Deviation of Runtimes: " << stdDeviation << endl;
    }


int main()
{
    vector<bool> remove_quotes = {false, false, true, true, false, false, true, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false};
    vector<Movie> movies = parseCSV("animated_movies.csv", remove_quotes);

    // Sort movies by popularity using merge sort
    movies = mergeSort(movies);

    // Print the top 5 movie titles with highest popularity
    cout << "Top 10 Movie Titles with Highest Popularity:\n";
    int count = 0;
    for (const Movie &movie : movies)
    {
        if (count >= 10)
            break;
        cout << movie.title << " - Popularity: " << movie.popularity << endl;
        count++;
    }
    languageDistribution(movies);
    analyzeRuntimeDistribution(runtimes);

    return 0;
}

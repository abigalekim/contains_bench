#include <DataFrame/DataFrame.h>
#include <DataFrame/DataFrameStatsVisitors.h>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <algorithm>

using namespace hmdf;
using StrDataFrame = StdDataFrame<std::string>;

int main(int argc, char** argv) {
  std::cout << "Filename: " + std::string(argv[1]) << std::endl;

  if (argc < 2) {
    std::cerr << "Error: did not pass enough arguments\n";
    return 0;
  }

  std::string request = "Harum Hic Ex At";
  auto contains_fn = [&request](const unsigned long&, const std::string& val) -> bool {
    return val.find(request) != std::string::npos;
  };
  std::string csv_filename = "/home/akkim7/string_datasets/" + std::string(argv[1]);
  std::vector<std::string> col_names = {"value"};

  StdDataFrame<unsigned long> df;
  std::ifstream file(csv_filename);
  std::vector<unsigned long> indices;
  std::vector<std::string> values;
  std::string line;
  unsigned long idx = 0;
  while (std::getline(file, line)) {
      if (!line.empty()) {
          line.erase(line.find_last_not_of(" \n\r\t") + 1);
          indices.push_back(idx++);
          values.push_back(line);
      }
  }
  file.close();
  df.load_data(std::move(indices), std::make_pair("value", values));

  {
    // cold run
    std::cout << "Running cold run...\n";
    auto result_df = df.get_data_by_sel<std::string, decltype(contains_fn), std::string>(
        "value", contains_fn);

    std::cout << "Running hot run...\n";
    auto start_time = std::chrono::high_resolution_clock::now();
    result_df = df.get_data_by_sel<std::string, decltype(contains_fn), std::string>(
        "value", contains_fn);
    auto end_time = std::chrono::high_resolution_clock::now();
  }

  float milliseconds_sum = 0.0f;
  for (int i = 0; i < 5; ++i) {
    auto start_time = std::chrono::high_resolution_clock::now();
    auto result_df = df.get_data_by_sel<std::string, decltype(contains_fn), std::string>(
        "value", contains_fn);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    milliseconds_sum += (duration.count() / 1000.0);
  }
  std::cout << "Contains query average: " << std::setprecision(5) << milliseconds_sum/5.0f << std::endl;
  return 0;
}
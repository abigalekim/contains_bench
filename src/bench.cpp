#include <rmm/mr/device/per_device_resource.hpp>
#include <rmm/mr/device/cuda_memory_resource.hpp>

#include <cudf/io/csv.hpp>
#include <cudf/table/table.hpp>
#include <cudf/utilities/error.hpp>
#include <cudf/strings/find.hpp>

#include <iostream>
#include <vector>
#include <string>
#include <memory>

int main(int argc, char** argv) {
  if (argc < 2) {
    std::cerr << "Error: did not pass enough arguments\n";
    return 0;
  }

  std::string request = "Harum Hic Ex At";
  std::string csv_filename = "/mnt/wiscdb/abigale/string_dataset_csvs/" + std::string(argv[1]);
  std::vector<std::string> col_names = {"value"};

  cudf::io::csv_reader_options options =
        cudf::io::csv_reader_options::builder(cudf::io::source_info(csv_filename))
        .names(col_names)
        .build();

    // 2. Read the CSV file into a table.
    std::unique_ptr<cudf::table> table;
    try {
        table = cudf::io::read_csv(options).tbl;
    } catch (const cudf::logic_error& e) {
        std::cerr << "Error reading CSV: " << e.what() << std::endl;
        return -1;
    }
    
    // 3. (Optional) Print some information about the table.
    if (table) {
        std::cout << "Successfully read CSV file." << std::endl;
        std::cout << "Number of columns: " << table->num_columns() << std::endl;
        std::cout << "Number of rows: " << table->num_rows() << std::endl;
    }

  
  return 0;
}
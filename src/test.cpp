#include <rmm/mr/device/per_device_resource.hpp>
#include <rmm/mr/device/cuda_memory_resource.hpp>
#include <rmm/mr/device/pool_memory_resource.hpp>

#include <cudf/io/csv.hpp>
#include <cudf/io/data_sink.hpp>
#include <cudf/table/table.hpp>
#include <cudf/utilities/error.hpp>
#include <cudf/strings/find.hpp>
#include <cudf/strings/attributes.hpp>

#include <iostream>
#include <vector>
#include <string>
#include <memory>

int main(int argc, char** argv) {
  if (argc < 2) {
    std::cerr << "Error: did not pass enough arguments\n";
    return 0;
  }

   // Check available GPU memory first
   size_t free_mem, total_mem;
   cudaMemGetInfo(&free_mem, &total_mem);
   std::cout << "GPU Memory - Total: " << total_mem / (1024*1024) << " MB, "
             << "Free: " << free_mem / (1024*1024) << " MB" << std::endl;

  auto cuda_mr = std::make_shared<rmm::mr::cuda_memory_resource>();

  // Create pool with much smaller initial allocation and reasonable max
  uint64_t initial_pool_size = 0UL;  // Start with 1GB
  uint64_t max_pool_size = 38UL * 1024UL * 1024UL * 1024UL;
  
  auto pool_mr = std::make_shared<rmm::mr::pool_memory_resource<rmm::mr::cuda_memory_resource>>(
      cuda_mr.get(),
      initial_pool_size,
      max_pool_size
  );
  
  rmm::mr::set_current_device_resource(pool_mr.get());

  std::cout << "Memory pool initialized: " 
            << initial_pool_size / (1024*1024) << " MB initial, "
            << max_pool_size / (1024*1024) << " MB max" << std::endl;

  std::string argument = std::string(argv[1]);
  std::string request;
  std::string output_filename = argument + ".txt";
  std::string csv_filename = "/home/ubuntu/string_datasets/";

  
  if (argument == "tpch") {
    request = "requests";
    csv_filename = csv_filename + "tpch_dataset.csv";
  } else if (argument == "wikipedia") {
    request = "probabilistic";
    csv_filename = csv_filename + "wikipedia_dataset.csv";
    
  } else if (argument == "synthetic") {
    request = "Omnis Possimus";
    csv_filename = csv_filename + "synthetic_dataset.csv";
  } else if (argument == "lineitem") {
    request = "requests";
    csv_filename = csv_filename + "lineitem.csv";
  } else {
    return 0;
  }
  
  std::vector<std::string> col_names = {"value"};

  cudf::io::csv_reader_options options =
    cudf::io::csv_reader_options::builder(cudf::io::source_info(csv_filename))
    .names(col_names)
    .delimiter('|')
    .build();

  std::unique_ptr<cudf::table> table;
  try {
      table = cudf::io::read_csv(options).tbl;
  } catch (const cudf::logic_error& e) {
      std::cerr << "Error reading CSV: " << e.what() << std::endl;
      return -1;
  }
    
  if (table) {
      std::cout << "Successfully read CSV file." << std::endl;
      std::cout << "Number of columns: " << table->num_columns() << std::endl;
      std::cout << "Number of rows: " << table->num_rows() << std::endl;
  }

  cudf::strings_column_view strings_col(table->get_column(0));

  // Print some statistics about your data
  std::cout << "Checking for empty/whitespace rows..." << std::endl;
    auto lengths = cudf::strings::count_characters(strings_col);

  // Copy to host memory
  std::vector<int32_t> host_lengths(lengths->size());
  cudaMemcpy(host_lengths.data(), 
            lengths->view().data<int32_t>(), 
            lengths->size() * sizeof(int32_t), 
            cudaMemcpyDeviceToHost);

  auto search_scalar = cudf::string_scalar(request);
  std::cout << "Performing contains query for: \"" << request << "\"" << std::endl;
  std::unique_ptr<cudf::column> result = cudf::strings::contains(strings_col, search_scalar);
  std::vector<std::unique_ptr<cudf::column>> columns;
  columns.push_back(std::move(result));
  auto result_table = std::make_unique<cudf::table>(std::move(columns));

  cudf::io::sink_info sink(output_filename);
  cudf::io::csv_writer_options write_options = 
      cudf::io::csv_writer_options::builder(sink, result_table->view())
          .include_header(false)
          .false_value("false")
          .build();
  
  cudf::io::write_csv(write_options);

  return 0;
}
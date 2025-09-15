#include <rmm/mr/device/per_device_resource.hpp>
#include <rmm/mr/device/cuda_memory_resource.hpp>
#include <rmm/mr/device/pool_memory_resource.hpp>

#include <cudf/io/csv.hpp>
#include <cudf/table/table.hpp>
#include <cudf/utilities/error.hpp>
#include <cudf/strings/find.hpp>

#include <iostream>
#include <vector>
#include <string>
#include <memory>

int main(int argc, char** argv) {
   // Check available GPU memory first
   size_t free_mem, total_mem;
   cudaMemGetInfo(&free_mem, &total_mem);
   std::cout << "GPU Memory - Total: " << total_mem / (1024*1024) << " MB, "
             << "Free: " << free_mem / (1024*1024) << " MB" << std::endl;

  auto cuda_mr = std::make_shared<rmm::mr::cuda_memory_resource>();

  // Create pool with much smaller initial allocation and reasonable max
  uint64_t initial_pool_size = 1UL * 1024UL * 1024UL * 1024UL;  // Start with 1GB
  uint64_t max_pool_size = 37UL * 1024UL * 1024UL * 1024UL;     // Max 16GB
  
  auto pool_mr = std::make_shared<rmm::mr::pool_memory_resource<rmm::mr::cuda_memory_resource>>(
      cuda_mr.get(),
      initial_pool_size,
      max_pool_size
  );
  
  rmm::mr::set_current_device_resource(pool_mr.get());
  std::cout << "Memory pool initialized: " 
            << initial_pool_size / (1024*1024) << " MB initial, "
            << max_pool_size / (1024*1024) << " MB max" << std::endl;

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
  auto search_scalar = cudf::string_scalar(request);
  std::cout << "Performing contains query for: \"" << request << "\"" << std::endl;
  auto start_time = std::chrono::high_resolution_clock::now();
  std::unique_ptr<cudf::column> result = cudf::strings::contains(strings_col, search_scalar);
  cudaDeviceSynchronize();
  auto end_time = std::chrono::high_resolution_clock::now();

  float milliseconds_sum = 0.0f;
  for (int i = 0; i < 5; ++i) {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::unique_ptr<cudf::column> result = cudf::strings::contains(strings_col, search_scalar);
    cudaDeviceSynchronize();
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    milliseconds_sum += (duration.count() / 1000.0);
  }
  std::cout << "Contains query average: " << std::setprecision(5) << milliseconds_sum/5.0f << std::endl;

  
  return 0;
}
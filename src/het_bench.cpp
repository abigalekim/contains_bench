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
  std::cout << "Filename: " + std::string(argv[1]) << std::endl;
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

  if (argc < 2) {
    std::cerr << "Error: did not pass enough arguments\n";
    return 0;
  }

  std::string request = "Harum Hic Ex At";
  std::string csv_filename = "/home/akkim7/string_datasets/" + std::string(argv[1]);
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

  cudf::strings_column_view strings_col(table->get_column(0));
  auto search_scalar = cudf::string_scalar(request);

  {
    // cold run
    std::cout << "Running cold run...\n";
    std::unique_ptr<cudf::column> result = cudf::strings::contains_heterogeneous(strings_col, search_scalar);
    cudaDeviceSynchronize();
  }

  float milliseconds_sum = 0.0f;
  for (int i = 0; i < 5; ++i) {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::unique_ptr<cudf::column> result = cudf::strings::contains_heterogeneous(strings_col, search_scalar);
    cudaDeviceSynchronize();
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    milliseconds_sum += (duration.count() / 1000.0);
  }
  std::cout << "Contains query average: " << std::setprecision(5) << milliseconds_sum/5.0f << std::endl;
  return 0;
}
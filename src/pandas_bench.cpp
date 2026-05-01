#include <Python.h>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <iomanip>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Error: did not pass enough arguments\n";
        return 0;
    }

    std::cout << "Filename: " << std::string(argv[1]) << std::endl;
    
    std::string csv_filename = "/home/akkim7/string_datasets/" + std::string(argv[1]);
    std::string request = "Harum Hic Ex At";

    // Initialize Python
    Py_Initialize();
    
    // Import pandas and numpy
    PyObject* pandas_module = PyImport_ImportModule("pandas");
    if (!pandas_module) {
        PyErr_Print();
        std::cerr << "Failed to import pandas\n";
        Py_Finalize();
        return -1;
    }

    // Read CSV
    PyObject* read_csv = PyObject_GetAttrString(pandas_module, "read_csv");
    PyObject* csv_args = Py_BuildValue("(s)", csv_filename.c_str());
    PyObject* csv_kwargs = Py_BuildValue("{s:s,s:[s]}", 
                                         "delimiter", "|",
                                         "names", "value");
    PyObject* df = PyObject_Call(read_csv, csv_args, csv_kwargs);
    
    if (!df) {
        PyErr_Print();
        std::cerr << "Failed to read CSV\n";
        Py_DECREF(csv_args);
        Py_DECREF(csv_kwargs);
        Py_DECREF(read_csv);
        Py_DECREF(pandas_module);
        Py_Finalize();
        return -1;
    }

    // Get the 'value' column
    PyObject* value_col = PyObject_GetItem(df, PyUnicode_FromString("value"));
    if (!value_col) {
        PyErr_Print();
        std::cerr << "Failed to get 'value' column\n";
        Py_DECREF(df);
        Py_DECREF(csv_args);
        Py_DECREF(csv_kwargs);
        Py_DECREF(read_csv);
        Py_DECREF(pandas_module);
        Py_Finalize();
        return -1;
    }

    // Get the str accessor
    PyObject* str_accessor = PyObject_GetAttrString(value_col, "str");
    if (!str_accessor) {
        PyErr_Print();
        std::cerr << "Failed to get str accessor\n";
        Py_DECREF(value_col);
        Py_DECREF(df);
        Py_DECREF(csv_args);
        Py_DECREF(csv_kwargs);
        Py_DECREF(read_csv);
        Py_DECREF(pandas_module);
        Py_Finalize();
        return -1;
    }

    // Get the contains method
    PyObject* contains_method = PyObject_GetAttrString(str_accessor, "contains");
    if (!contains_method) {
        PyErr_Print();
        std::cerr << "Failed to get contains method\n";
        Py_DECREF(str_accessor);
        Py_DECREF(value_col);
        Py_DECREF(df);
        Py_DECREF(csv_args);
        Py_DECREF(csv_kwargs);
        Py_DECREF(read_csv);
        Py_DECREF(pandas_module);
        Py_Finalize();
        return -1;
    }

    // Cold run
    std::cout << "Running cold run...\n";
    PyObject* contains_args = Py_BuildValue("(s)", request.c_str());
    PyObject* result_cold = PyObject_CallObject(contains_method, contains_args);
    if (!result_cold) {
        PyErr_Print();
        Py_DECREF(contains_args);
        Py_DECREF(contains_method);
        Py_DECREF(str_accessor);
        Py_DECREF(value_col);
        Py_DECREF(df);
        Py_DECREF(csv_args);
        Py_DECREF(csv_kwargs);
        Py_DECREF(read_csv);
        Py_DECREF(pandas_module);
        Py_Finalize();
        return -1;
    }
    Py_DECREF(result_cold);

    // Hot run
    std::cout << "Running hot run...\n";
    auto start_time = std::chrono::high_resolution_clock::now();
    PyObject* result_hot = PyObject_CallObject(contains_method, contains_args);
    auto end_time = std::chrono::high_resolution_clock::now();
    if (!result_hot) {
        PyErr_Print();
    }
    Py_XDECREF(result_hot);

    // Benchmark runs
    float milliseconds_sum = 0.0f;
    for (int i = 0; i < 5; ++i) {
        start_time = std::chrono::high_resolution_clock::now();
        PyObject* result = PyObject_CallObject(contains_method, contains_args);
        end_time = std::chrono::high_resolution_clock::now();
        
        if (!result) {
            PyErr_Print();
            continue;
        }
        Py_DECREF(result);
        
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
        milliseconds_sum += (duration.count() / 1000.0);
    }

    std::cout << "Contains query average: " << std::setprecision(5) << milliseconds_sum/5.0f << " ms" << std::endl;

    // Cleanup
    Py_DECREF(contains_args);
    Py_DECREF(contains_method);
    Py_DECREF(str_accessor);
    Py_DECREF(value_col);
    Py_DECREF(df);
    Py_DECREF(csv_args);
    Py_DECREF(csv_kwargs);
    Py_DECREF(read_csv);
    Py_DECREF(pandas_module);
    
    Py_Finalize();
    return 0;
}
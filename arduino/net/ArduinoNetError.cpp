#include <iostream>
#include <exception>
#include "ArduinoNetError.h"

class ArduinoNetError : public std::exception {
const char* file;
int line;
const char* func;
const char* info;
    
public:
 	ArduinoNetError(const char* msg, const char* file_, int line_,
 		const char* func_, const char* info_ = "") : std::exception(msg),
     	file (file_),
     	line (line_),
     	func (func_),
     	info (info_)
      {
      }
        
  const char* get_file() const { return file; }
  int get_line() const { return line; }
	const char* get_func() const { return func; }
  const char* get_info() const { return info; }
       
}

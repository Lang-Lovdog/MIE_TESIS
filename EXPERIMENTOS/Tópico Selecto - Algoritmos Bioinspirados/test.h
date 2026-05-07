#ifdef __linux__
#include <unistd.h>
void descansa(void) { sleep(1); }
#endif

typedef struct TuningVars{
  long double constriccion;
  long double clamping;
  long double inertia;
  long double c1;
  long double c2;
  unsigned int max_iter;
  unsigned int cant_part;
  unsigned int cant_dim;
  unsigned int execution_times;
}TuningVars;


void parse_opts(int argc, char *argv[], TuningVars *tuning_vars);
void initialize_options(TuningVars *tuning_vars);
void help(void);

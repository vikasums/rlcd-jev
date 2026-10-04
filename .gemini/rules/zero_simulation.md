# Rule: Zero Simulation & Live Local Execution Directive

1. **Live Local Execution Only**: Always execute live, real, non-simulated benchmarks and evaluations (e.g., live Microsoft Presidio `AnalyzerEngine()`, live JailbreakBench datasets, live local Ollama model calls).
2. **No Fallback Simulations**: Never fall back to simulated or dummy fallback data when errors occur during execution.
3. **Prompt User on Errors**: If an API, dataset download, or library call encounters an error, stop immediately, display the un-truncated error, and ask the user for guidance before taking any further action.

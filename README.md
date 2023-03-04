# Assignment 1 for CE4046: Intelligent Agents

## Getting Started

1. Install requirements
```
pip install requirements.txt 
```
2. Run Code
```
python main.py --algorithm=value_iteration --random_grid=False --debug=False
```
Options:
- Algorithm: Select between value iteration or policy iteration  
`value_iteration` | `policy_iteration`
- Random Grid: Use grid for Task 1 (False) or generate a new random grid  
`True` | `False`  
*Note: Random seed is set to 1 in `config.py`. Change value to generate different grid.*
- Debug: Print debug statements in command line  
`True` | `False`  
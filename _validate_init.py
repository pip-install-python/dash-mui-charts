"""Validate that all Python components have been generated."""
import sys
import dash_mui_charts

if __name__ == '__main__':
    print('dash_mui_charts version:', dash_mui_charts.__version__)
    print('Components:', dash_mui_charts.__all__)

    # Check if LineChart is available
    if hasattr(dash_mui_charts, 'LineChart'):
        print('LineChart component: OK')
    else:
        print('ERROR: LineChart component not found!')
        sys.exit(1)

    print('Validation passed!')

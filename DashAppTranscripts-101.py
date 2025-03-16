import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import os
import pandas as pd

# Directories
TRANSCRIPTS_DIR = "./transcripts"
SOURCE_DIR = "./transcriptsource"
SUMMARY_DIR = "./transcriptsummary"
PROCESSED_DIR = "./transcriptprocessed"

CA_Blue = '#004B88'

# Initialize Dash app
app = dash.Dash(__name__)

# Get list of CSV files in transcripts folder
# csv_files = [f[0:12] for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith('.csv')]
csv_files = []
for i in range(0,20):
    csv_files.append(f"Example-{i:04d}")

def read_csv_file(file_path):
    """Read CSV and return DataFrame"""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

def read_text_file(file_path):
    """Read text file contents"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return str(e)

# App layout
app.layout = html.Div([

    html.Div([
        html.Img(src='/assets/CA-Logo.png', style={'height': '100px', 'marginRight': '10px'}),
        html.H1("Call Summarisation", style={"textAlign": "left", "color": "white", "flexGrow": "1"})
    ], style={'display': 'flex', 'alignItems': 'center', 'backgroundColor': CA_Blue, 'padding': '10px'}),
 
    html.Div([
        html.H3("Choose an Example Transcript"),
        dash_table.DataTable(
            id='file-table',
            columns=[{"name": "File Name", "id": "File Name"}],
            data=[{"File Name": f} for f in csv_files],
            row_selectable='single',
            style_table={'width': '100%', 'border': '1px solid black', "textAlign": "left"},
            style_cell={'textAlign': 'left'}  # Left-aligns text in all cells
        )
    ], style={'width': '15%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div(style={'width': '10%', 'display': 'inline-block'}),  # Blank space between columns
    
    html.Div([
        html.H3("Transcript From Call"),
        html.Pre(id='source-content', style={"border": "1px solid blue", "padding": "10px", "height": "100px", "overflowY": "auto"}),

        html.H3("Transcript Prepared for Summarisation"),
        dcc.Textarea(
            id='processed-content',
            style={
                'width': '100%', 
                'height': '100px', 
                'whiteSpace': 'pre-wrap',  # Ensures text wraps
                'overflowY': 'auto'  # Enables scrolling if needed
            }
        ),

        html.H3("Transcript Summary from BedRock MISTRAL"),
        dcc.Textarea(
            id='summary-content',
            style={
                'width': '100%', 
                'height': '100px', 
                'whiteSpace': 'pre-wrap',  # Ensures text wraps
                'overflowY': 'auto'  # Enables scrolling if needed
            }
        ),
    ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginTop': '20px'})
])

@app.callback(
    [Output('source-content', 'children'),
     Output('summary-content', 'value'),
     Output('processed-content', 'value')],
    Input('file-table', 'selected_rows')
)
def update_contents(selected_rows):
    if selected_rows is None or len(selected_rows) == 0:
        return "Select a file", "Select a file", "Select a file"
    
    selected_file = csv_files[selected_rows[0]]
    source_path = os.path.join(SOURCE_DIR, f'{selected_file}.csv')
    summary_path = os.path.join(SUMMARY_DIR, f'{selected_file}.txt')
    processed_path = os.path.join(PROCESSED_DIR, f'{selected_file}.txt')
    
    source_text = read_text_file(source_path)
    summary_text = read_text_file(summary_path)
    processed_text = read_text_file(processed_path)
    
    return source_text, summary_text, processed_text

if __name__ == '__main__':
    app.run_server(debug=True)

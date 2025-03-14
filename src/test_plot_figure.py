from plot_figure import *

output_dir = Path(config("OUTPUT_DIR"))

def test_plot_figure():
    """Test with dummy DataFrame, and check if it saves the correct name in the dir
    """
    # Create dict for DataFrame
    arb_df = {}
    col = []
    start = pd.Timestamp(config("START_DATE")).date()
    arb_df[start] = [x for x in range(7)]
    arb_df[pd.Timestamp('2010-02-01').date()] = [x for x in range(7, 14)]
    for year in [1,20,2,30,3,5,10]:
        col.append(f'Arb_Swap_{year}')
    arb_df = pd.DataFrame.from_dict(arb_df, orient = 'index', columns = col)

    file = os.path.join(output_dir, "dummy_plot.png")
    
    plot_figure(arb_df, file)

    assert os.path.exists(file)

def test_plot_main():
    """Runs plot_main() and checks if the plots are saved correctly
    Note: It only passes/works when running with a bloomberg-enabled machine.
    """
    plot_main()
    file_r = os.path.join(output_dir, 'replicated_swap_spread_arb_figure.png')
    file_u = os.path.join(output_dir, 'updated_swap_spread_arb_figure.png')
    assert os.path.exists(file_r) and os.path.exists(file_u)
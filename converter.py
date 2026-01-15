import pandas as pd
import flowio
import numpy as np
import os

class DataConverter:
    @staticmethod
    def convert_to_parquet(file_path, output_path, options=None):
        """
        Converts a single file (FCS, CSV, TSV) to Parquet.
        
        Args:
            file_path (str): Path to input file.
            output_path (str): Path to output parquet file.
            options (dict): Configuration options.
                - use_marker_names (bool): For FCS, use PnS (Marker) as column name if available.
                - add_filename_col (bool): Add a column with the filename (useful for merging).
                - compression (str): 'snappy', 'gzip', 'brotli', or None.
        """
        if options is None:
            options = {}

        df, error = DataConverter._read_file_to_df(file_path, options)
        if error:
            return False, error

        try:
            # Write to parquet
            compression = options.get('compression', 'snappy')
            df.to_parquet(output_path, index=False, compression=compression)
            return True, f"Successfully converted to {os.path.basename(output_path)}"

        except Exception as e:
            return False, str(e)

    @staticmethod
    def combine_to_parquet(file_paths, output_path, options=None):
        """
        Combines multiple files into a single Parquet file.
        """
        if options is None:
            options = {}
        
        dfs = []
        for fp in file_paths:
            df, error = DataConverter._read_file_to_df(fp, options)
            if error:
                return False, f"Error reading {os.path.basename(fp)}: {error}"
            dfs.append(df)
            
        if not dfs:
            return False, "No data found."
            
        try:
            combined_df = pd.concat(dfs, ignore_index=True)
            compression = options.get('compression', 'snappy')
            combined_df.to_parquet(output_path, index=False, compression=compression)
            return True, f"Successfully combined {len(file_paths)} files to {os.path.basename(output_path)}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _read_file_to_df(file_path, options):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.fcs':
                df = DataConverter._read_fcs(file_path, options)
            elif ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext == '.tsv':
                df = pd.read_csv(file_path, sep='\t')
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path)
            else:
                return None, f"Unsupported file format: {ext}"

            # Add filename column if requested
            if options.get('add_filename_col', False):
                sample_id = os.path.splitext(os.path.basename(file_path))[0]
                df.insert(0, 'SampleID', sample_id)
            
            return df, None
        except Exception as e:
            return None, str(e)


    @staticmethod
    def _read_fcs(file_path, options):
        fd = flowio.FlowData(file_path)
        events = np.reshape(fd.events, (-1, fd.channel_count))
        
        channels = {}
        # Parse channels logic similar to FlowJo/OMIQ standard expectation
        for i in range(1, fd.channel_count + 1):
            # Try to find PnN (Name) and PnS (Desc/Marker)
            # FlowIO text segment parsing
            pnn = fd.text.get(f'P{i}N', f'P{i}N') # Default key lookup
            pns = fd.text.get(f'P{i}S', None)
            
            # Helper to check various case-sensitivities if standard lookup fails
            if not pnn: 
                # Scan keys case-insensitive
                for k, v in fd.text.items():
                    if k.upper() == f'P{i}N':
                        pnn = v
                        break
            
            if not pns:
                for k, v in fd.text.items():
                    if k.upper() == f'P{i}S':
                        pns = v
                        break

            # Decide column name
            use_marker = options.get('use_marker_names', True)
            if use_marker and pns and str(pns).strip() != "":
                col_name = f"{pns} ({pnn})" if pnn != pns else pns
                # Simpler: often people just want "CD4", not "CD4 (FL1-H)"
                # Let's check a "clean_names" option or default to PnS
                # If PnS exists, use it. If duplicates arise, append PnN.
                col_name = pns
            else:
                col_name = pnn
            
            channels[i-1] = col_name

        # Create DataFrame
        df = pd.DataFrame(events)
        
        # Assign columns and handle duplicates
        col_names = [channels[i] for i in range(len(channels))]
        
        # Dedup column names if necessary (e.g., two "Unstained" channels)
        final_cols = []
        seen = {}
        for c in col_names:
            if c in seen:
                seen[c] += 1
                final_cols.append(f"{c}_{seen[c]}")
            else:
                seen[c] = 0
                final_cols.append(c)
                
        df.columns = final_cols
        return df

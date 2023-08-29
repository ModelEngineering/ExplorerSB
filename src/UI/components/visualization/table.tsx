import { DisplayMode } from "../visualization";
import DataTable from 'rc-table';

// Define the Table component
const Table = ({
  data,
  xVariable,
  variables,
  displayMode
}: {
  data: Object[];
  xVariable: string | undefined;
  variables: VariableSelectOption[];
  displayMode: DisplayMode;
}) => {
  // Initialize an array to store column configurations for the table
  const columns: Record<string, any>[] = [];

  // If an xVariable is provided, create a column for it in the table
  if (xVariable !== undefined) {
    columns.push({
      title: xVariable,
      dataIndex: xVariable,
      key: xVariable,
      render: (value: number) => parseFloat(value.toPrecision(4)) // Format the value for display
    });
  }

  // Create columns for other variables in the 'variables' array
  variables.forEach((variable) => {
    columns.push({
      title: variable.name,
      dataIndex: variable.name,
      key: variable.name,
      render: (value: number) => {
        // Conditionally format the value based on its magnitude
        if (Math.abs(value) < 1e-4) {
          return parseFloat(value.toPrecision(4));
        } else {
          return parseFloat(value.toFixed(4));
        }
      }
    });
  });

  return (
    <div id="table-container" className={displayMode === DisplayMode.Table ? "" : "hidden"}>
      {/* Display a message if no data is available */}
      {data.length === 0 ? (
        <p>Table not Available</p>
      ) : (
        // Render the DataTable component with configured columns and data
        <DataTable columns={columns} data={data} rowKey={(record, index) => record.toString() + index} />
      )}
    </div>
  );
};

export default Table; // Export the Table component

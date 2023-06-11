import { DisplayMode } from "../Visualization";
import DataTable from 'rc-table';

const Table = ({data, xVariable, variables, displayMode}: {data: Object[], xVariable: string | undefined, variables: VariableSelectOption[], displayMode: DisplayMode}) => {
  const columns : Record<string, any>[] = []
  if(xVariable !== undefined) {
    columns.push({
      title: xVariable,
      dataIndex: xVariable,
      key: xVariable,
      render: (value: number) => parseFloat(value.toPrecision(4)),
    })
  }
  variables.forEach((variable) => {
    columns.push({
      title: variable.name,
      dataIndex: variable.name,
      key: variable.name,
      render: (value: number) => {
        if(Math.abs(value) < 1e-4) 
        { 
          return parseFloat(value.toPrecision(4))
        }
        else {
          return parseFloat(value.toFixed(4))
        }
      },
    })
  })
  return (
  <div id="table-container" className={displayMode === DisplayMode.Table ? "" : "hidden"}>
    {data.length === 0 ? 
    <p>Table not Available</p> :
    <DataTable columns={columns} data={data} rowKey={(record, index) => record.toString() + index} />}
  </div>
  )
}

export default Table;
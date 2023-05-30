import { DisplayMode } from "../Visualization";
import DataTable from 'rc-table';

const Table = ({data, xVariable, variables, displayMode}: {data: Object[], xVariable: string | undefined, variables: { name: string }[], displayMode: DisplayMode}) => {
  const columns : Record<string, any>[] = []
  if(xVariable !== undefined) {
    columns.push({
      title: xVariable,
      dataIndex: xVariable,
      key: xVariable,
    })
  }
  variables.forEach((variable) => {
    columns.push({
      title: variable.name,
      dataIndex: variable.name,
      key: variable.name,
    })
  })
  return (
  <div id="table-container" className={displayMode === DisplayMode.Table ? "" : "hidden"}>
    {data.length === 0 ? 
    <p>Table not Available</p> :
    <DataTable columns={columns} data={data} rowKey={(record, index) => record.toString() + index}/>}
  </div>
  )
}

export default Table;
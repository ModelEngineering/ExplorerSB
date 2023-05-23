import { DisplayMode } from "../Visualization";

const Table = ({data, variables, displayMode}: {data: Object[], variables: Object[], displayMode: DisplayMode}) => {
  return (
  <div id="table-container" className={displayMode === DisplayMode.Table ? "" : "hidden"}>
    {data.length === 0 ? <p>Table not Available</p> :
    <table>
      {variables.map((variable: any) => (
        <tr>
            <th>{variable.name}</th>
            {data.map((data: any) => {
              return <td>{data[variable.name]} </td>
            })}
        </tr>
      ))}
      </table>}
  </div>
  )
}

export default Table;
import { DisplayMode } from "../Visualization";

const Table = ({data, variables, displayMode}: {data: Object[], variables: Object[], displayMode: DisplayMode}) => {
  return (
  <div id="table-container" className={displayMode === DisplayMode.Table ? "" : "hidden"}>
    {data.length === 0 ? <p>Table not Available</p> :
    <table>
      <tbody>
      {variables.map((variable: any, index) => (
        <tr key={`row-${index}`}>
            <th>{variable.name}</th>
            {data.map((data: any, indexInner) => {
              return <td key={`item-${indexInner}`}>{data[variable.name]} </td>
            })}
        </tr>
      ))}
      </tbody>
    </table>}
  </div>
  )
}

export default Table;
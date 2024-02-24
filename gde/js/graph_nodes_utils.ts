import axios from "axios"
import type {NodeInformationSchema} from "./type_defs.ts"

export function getEdgeColor(node: NodeInformationSchema) {
  if (node._meta.hasOwnProperty('display_type') && node._meta.display_type == 'color')
    return node._meta.display_value
  else
    return 'white'
}

export function getNodeColor(node: NodeInformationSchema) {
  if (node._meta.display_type){
    if (node._meta.display_type == 'color')
      return node._meta.display_value
    else
      return '#1b1b1b'
  } else {
    return 'white'
  }
}

export async function getNodeTypes() {
  const url = import.meta.env.VITE_API_BASE_URL + '/node-types';
  const response = await axios.get(url);

  if (response.status !== 200) {
    console.log("error:", response.statusText, response)
  }

  // convert response.data list to an object with attribute name fetched from lists element _key
  const nodeTypes = response.data.map(x => ({ [x._key]: x }))
  .reduce((acc, curr) => {
    Object.assign(acc, curr);
    return acc;
  }, {});

  return nodeTypes

}
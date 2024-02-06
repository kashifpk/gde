function getNodeDisplay(node) {

  console.log("Node display processing: ", node)
  if (node._meta.hasOwnProperty('display_type') && node._meta.display_type == 'color')
    return node._meta.display_value
  else
    return 'white'
}

export { getNodeDisplay };
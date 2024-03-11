
export interface NodeMetaInformation {
  node_type: string | null
  label: string | null
  display_type: 'color' | 'icon' | 'image' | null
  display_value: string | null
}


export interface LinkInfo {
  _key: string
  source: string
  target: string
  _meta: NodeMetaInformation
  linked_node: NodeInformationSchema
}

export interface NodeInformationSchema {
  _key: string
  _meta: NodeMetaInformation
  extra_info: object
  _links: (LinkInfo | null)[]
  [x: string]: unknown  // allow extra fields
}

export interface FieldsData {
  node_type?: string | null
  [name: string]: string | object | NodeMetaInformation
}

export interface FieldSpecification {
  name: string
  label?: string | null
  data_type?: string | null
  required?: boolean | null
  content_type?: string | null
  choices?: any[] | null
  [x: string]: unknown  // allow extra fields
}

export interface FieldsMap {
  [name: string]: FieldSpecification
}
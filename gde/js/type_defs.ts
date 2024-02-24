
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
    _meta: NodeInformationSchema
    linked_node: NodeInformationSchema
}

export interface NodeInformationSchema {
    _key: string
    _meta: NodeMetaInformation
    extra_info: object
    _links: (LinkInfo | null)[]
    [x: string]: unknown  // allow extra fields
}

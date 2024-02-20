// { "node_type": "person", "label": "Bajwa", "display_type": "image", "display_value": "/static/gmedia/images/bajwa.jpg" }

export interface NodeMetaInformation {
    node_type: string | null
    label: string | null
    display_type: 'color' | 'icon' | 'image' | null
    display_value: string | null
}


export interface NodeInformationSchema {
    _key: string
    _meta: NodeMetaInformation
    extra_info: object
    _links: (string | null)[]
    [x: string]: unknown  // allow extra fields
}

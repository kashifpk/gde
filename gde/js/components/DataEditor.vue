<style>
  /* Component Documentation
  Display data and allow editing the data. Allows dynamically adding and removing fields and JSON view of data.
  */
</style>

<template>
  <v-container v-if="props.fields.length > 0">
    <v-row v-for="field in fields">
      <v-col>
        <Field
          :label="field.label || field.name"
          :content-type="fieldsByKey[field.name].content_type"
          v-model="fieldsData[field.name]"
          @update:model-value="updateModelValue(field.name)"
          :initial-mode="props.initialMode"
          :required="field.required || false"
          :choices="field.choices || []" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">

  import { onMounted, ref, watch} from "vue"
  import type {FieldSpecification, FieldsData, FieldsMap} from "../type_defs.ts"
  import Field from "./Field.vue"

  interface Props {
    fields: FieldSpecification[]
    modelValue: object
    initialMode: string
  }
  const props = withDefaults(defineProps<Props>(), { initialMode: "view"})

  const emit = defineEmits(['update:modelValue', 'cancel', 'save'])

  const fieldsByKey: FieldsMap = {}
  const fieldsData = ref<FieldsData>({})
  const currentMode = ref("view")

  const dataToContentTypeMap = {
    "string": "text",
    "object": "json",
    "array": "json",
    "boolean": "checkbox"
  }

  watch(
    () => props.fields,
    (newValue, oldValue) => {
      if (newValue.length > 0) {
        for(const field of props.fields) {

          console.log(field)

          if (field.data_type == "object") {
            fieldsData.value[field.name] = JSON.stringify(props.modelValue[field.name], null, 2)
          } else {
            fieldsData.value[field.name] = props.modelValue[field.name]
          }

          let newField = {...field}
          if (!newField.content_type)
            newField.content_type = dataToContentTypeMap[field.data_type]
          fieldsByKey[field.name] = newField

          if (props.modelValue[field.name] == undefined) {
            console.log(field.name, "is undefined")
            props.modelValue[field.name] = ""
            if (fieldsByKey[field.name].content_type == "json"){
              if (field.data_type == "object")
                props.modelValue[field.name] = {}
              else if (field.data_type == "array")
                props.modelValue[field.name] = []
            }


          }

        }

        console.log("Fields By Key", fieldsByKey)
      }
    },
    { deep: true }
  )

  onMounted(() => {
    currentMode.value = props.initialMode
  })

  const updateModelValue = (fieldName: string) => {
    console.log("In updateModelValue.")
    console.log(" Fields length: ", props.fields.length)

    if (props.fields.length > 0) {
      let newValue = fieldsData.value[fieldName]
      if (fieldsByKey[fieldName]?.data_type == 'object') {
        try {
          newValue = JSON.parse(newValue)
          console.log("Emitting after string to object conversion", newValue)
          emit('update:modelValue', { ...props.modelValue, [fieldName]: newValue })
        } catch (error) {

          //console.log(error)
        }
      }else{
        console.log("Emitting without modification", newValue)
        emit('update:modelValue', { ...props.modelValue, [fieldName]: newValue })
      }


    }
  }
</script>




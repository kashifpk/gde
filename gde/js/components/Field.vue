<style scoped>

.field-wrapper {
  min-width: 14em;
  width: 100%;
}
.gde-display {
  color:#eee;
  padding: 5px 10px;
}

.gde-field {
  position: relative;
  padding: 5px 10px;
}
.gde-field input {
  background-color: rgb(57, 57, 57);
  padding: 3px 10px;
  box-sizing: border-box;
  border: 2px solid rgb(108, 108, 108);
  border-radius: 5px;
  outline-style: none;

}

.input-with-label, select {
  width: 80%;
}

.input-without-label {
  width: 100%;
}

.gde-field input[type=text]:focus {
  border: 2px solid #787878;
  background-color: rgb(42, 42, 42);
}

.normal-text {
  color: #eee
}
.dimmed-text {
  color: #8b8b8b
}


.label-in-border {
  position: absolute;
  top: -0.8em;
  z-index: 1;
  left: 1em;
  background-color: rgb(42, 42, 42);
  padding: 0 5px;
  font-size: smaller;
}

.side-label {
  width: 20%;
}

</style>

<template>
  <div class="field-wrapper">
    <div v-if="displayMode=='view'" class="gde-display" @click="switchToEditMode()">
      <label v-if="props.noSeparateLabel==false"
             :class="[props.noSeparateLabel==true ? 'label-in-border' : 'side-label']">
        {{ props.label }}
      </label>
      {{ inputValue }}
    </div>
    <div v-if="displayMode=='edit'" class="gde-field">
      <label v-if="!labelBeingDisplayedInContent"
             :class="[props.noSeparateLabel==true ? 'label-in-border' : 'side-label']"
             >
        {{ props.label }}
      </label>
      <input v-if="props.choices.length == 0"
        type="text"
        ref="inputFieldRef"
        :class="[props.modelValue=='' ? 'dimmed-text' : 'normal-text', props.noSeparateLabel==true ? 'input-without-label' : 'input-with-label']"
        :value="inputValue"
        @input="emit('update:modelValue', $event.target.value)"
        @focusin="onFocus()"
        @focusout="onFocusLost()"
        />

      <select v-if="props.choices.length > 0"
        size="1"
        :value="inputValue"
        @change="emit('update:modelValue', $event.target.value)">
        <option v-if="props.required == false"></option>
        <option v-for="choice in props.choices">{{ choice }}</option>
      </select>
    </div>
  </div>


</template>

<script setup>
  import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"


  const emit = defineEmits(['update:modelValue'])
  const props = defineProps({
    modelValue: {
      type: String,
      required: true
    },
    label: {
      type: String,
      default: ""
    },
    noSeparateLabel: {
      type: Boolean,
      default: false
    },
    initialMode: {
      type: String,
      default: "view"
    },
    choices: {  // choices array, if present makes the field a drop down
      type: Array,
      default: []
    },
    required: {
      type: Boolean,
      default: false
    }
  })

  const displayMode = ref("view")
  const inputHasFocus = ref(false)
  const labelBeingDisplayedInContent = ref(false)
  const inputFieldRef = ref()
  const switchToViewModeOnLostFocus = ref(true)

  const inputValue = computed(() => {
    if (props.noSeparateLabel==false) {
      labelBeingDisplayedInContent.value = false
      return props.modelValue
    }

    if (props.modelValue == "") {

      if (inputHasFocus.value == true) {
        labelBeingDisplayedInContent.value = false
        return ""
      } else {
        labelBeingDisplayedInContent.value = true
        return props.label
      }

    } else {
      labelBeingDisplayedInContent.value = false
      return props.modelValue
    }
  })

  onMounted(() => {
    displayMode.value = props.initialMode
    if (props.initialMode != 'view') {
      switchToViewModeOnLostFocus.value = false
    }
  })

  const onFocus = () => {
    inputHasFocus.value = true
  }

  const switchToEditMode = async () => {
    if (displayMode.value == 'edit') {
      return
    }

    displayMode.value = 'edit'
    await nextTick()
    // console.log(inputFieldRef.value)
    inputFieldRef.value.focus()
  }

  const onFocusLost = () => {
    if (switchToViewModeOnLostFocus.value == true) {
      inputHasFocus.value = false
      displayMode.value = 'view'
    }
  }



</script>

import {MonsterAttribute} from "@/enums/MonsterAttribute";
import React from "react";
import {observer} from "mobx-react-lite";
import {useStore} from "@/state";

interface PresetAttributeButtonProps {
  attr: MonsterAttribute;
}

const PresetAttributeButton: React.FC<PresetAttributeButtonProps> = observer((props) => {
  const store = useStore();
  const {monster, prefs} = store;
  const {attr} = props;

  const isSelected = monster.attributes.includes(attr);

  return (
    <button
      disabled={!prefs.manualMode}
      className={`rounded px-1 transition-[background,color] ${isSelected ? 'bg-blue-600 text-white' : 'bg-body-100 dark:bg-dark-200 opacity-50 dark:opacity-25 hover:enabled:bg-body-200 dark:hover:enabled:bg-dark-200'}`}
      onClick={() => store.toggleMonsterAttribute(attr)}
    >
      {attr}
    </button>
  )
})

export default PresetAttributeButton;

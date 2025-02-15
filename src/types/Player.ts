import {EquipmentCategory} from '@/enums/EquipmentCategory';
import {Prayer} from '@/enums/Prayer';
import {Potion} from '@/enums/Potion';
import {Spell} from '@/types/Spell';
import {PlayerCombatStyle} from "@/types/PlayerCombatStyle";

export interface PlayerSkills {
  atk: number;
  def: number;
  hp: number;
  magic: number;
  prayer: number;
  ranged: number;
  str: number;
}

export interface EquipmentPiece {
  name: string;
  id: number;
  version: string;
  slot: string;
  image: string;
  speed: number;
  category: EquipmentCategory;
  offensive: number[],
  defensive: number[],
  isTwoHanded: boolean;
}

/**
 * Each slot is represented by an item ID. We've used a string rather than a number here to represent the IDs in case
 * we have to use strings in the future (for arbitrary, non-ID values).
 */
export interface PlayerEquipment {
  head: EquipmentPiece | null;
  cape: EquipmentPiece | null;
  neck: EquipmentPiece | null;
  ammo: EquipmentPiece | null;
  weapon: EquipmentPiece | null;
  body: EquipmentPiece | null;
  shield: EquipmentPiece | null;
  legs: EquipmentPiece | null;
  hands: EquipmentPiece | null;
  feet: EquipmentPiece | null;
  ring: EquipmentPiece | null;
}

export interface PlayerBonuses {
  str: number;
  ranged_str: number;
  magic_str: number;
  prayer: number;
}

export interface PlayerDefensive {
  stab: number;
  slash: number;
  crush: number;
  magic: number;
  ranged: number;
}

export interface PlayerOffensive {
  stab: number;
  slash: number;
  crush: number;
  magic: number;
  ranged: number;
}

export interface Player {
  style: PlayerCombatStyle;
  /**
   * The player's base skill levels. These are their skill levels before any boosts (for example, from potions)
   * are applied.
   */
  skills: PlayerSkills;
  /**
   * These are the values for each skill that should be added to each of the "skills" property's values to compute
   * the player's "current" skill levels.
   */
  boosts: PlayerSkills;
  equipment: PlayerEquipment;
  prayers: Prayer[];
  bonuses: PlayerBonuses;
  defensive: PlayerDefensive;
  offensive: PlayerOffensive;
  buffs: {
    /**
     * This property should only be used to display the UI state, and should not be used in calculator code.
     *
     * Instead, use the "boosts" value of the Player interface, which contains the computed value that should be
     * added to each of the "skills" values to make the player's "current" skill levels.
     */
    potions: Potion[];
    onSlayerTask: boolean;
    inWilderness: boolean;
    /**
     * Whether the Kandarin Hard Diary has been completed, which provides 10% increase for the enchanted bolt spec to activate.
     * @see https://oldschool.runescape.wiki/w/Kandarin_Diary#Hard
     */
    kandarinDiary: boolean;
    /**
     * Whether the Charge spell buff is being used, which empowers god spells from the Mage Arena.
     * @see https://oldschool.runescape.wiki/w/Charge
     */
    chargeSpell: boolean;
    /**
     * Whether the Mark of Darkness spell buff is being used, which boosts the effect of Arceuus spells.
     * @see https://oldschool.runescape.wiki/w/Mark_of_Darkness
     */
    markOfDarknessSpell: boolean;
  }
  spell: Spell
}

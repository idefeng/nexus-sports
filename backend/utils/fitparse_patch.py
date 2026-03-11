"""
Monkey-patch for fitparse to workaround invalid Coros FIT files.
"""
import fitparse
from fitparse.base import BASE_TYPES, BASE_TYPE_BYTE, FitParseError
from fitparse.base import FieldDefinition, DevFieldDefinition, DefinitionMessage, get_dev_type, MESSAGE_TYPES

def patched_parse_definition_message(self, header):
    """
    Patched method to replace `fitparse.FitFile._parse_definition_message`,
    falling back to byte array instead of raising FitParseError when size doesn't match.
    """
    endian = '>' if self._read_struct('xB') else '<'
    global_mesg_num, num_fields = self._read_struct('HB', endian=endian)
    mesg_type = MESSAGE_TYPES.get(global_mesg_num)
    field_defs = []

    for n in range(num_fields):
        field_def_num, field_size, base_type_num = self._read_struct('3B', endian=endian)
        field = mesg_type.fields.get(field_def_num) if mesg_type else None
        base_type = BASE_TYPES.get(base_type_num, BASE_TYPE_BYTE)

        if (field_size % base_type.size) != 0:
            # FIX FOR COROS / WAHOO: Fallback to byte encoding instead of throwing
            base_type = BASE_TYPE_BYTE

        if field and field.components:
            for component in field.components:
                if component.accumulate:
                    accumulators = self._accumulators.setdefault(global_mesg_num, {})
                    accumulators[component.def_num] = 0

        field_defs.append(FieldDefinition(
            field=field,
            def_num=field_def_num,
            base_type=base_type,
            size=field_size,
        ))

    dev_field_defs = []
    if header.is_developer_data:
        num_dev_fields = self._read_struct('B', endian=endian)
        for n in range(num_dev_fields):
            field_def_num, field_size, dev_data_index = self._read_struct('3B', endian=endian)
            field = get_dev_type(dev_data_index, field_def_num)
            dev_field_defs.append(DevFieldDefinition(
                field=field,
                dev_data_index=dev_data_index,
                def_num=field_def_num,
                size=field_size
              ))

    def_mesg = DefinitionMessage(
        header=header,
        endian=endian,
        mesg_type=mesg_type,
        mesg_num=global_mesg_num,
        field_defs=field_defs,
        dev_field_defs=dev_field_defs,
    )
    self._local_mesgs[header.local_mesg_num] = def_mesg
    return def_mesg

def apply_patch():
    fitparse.FitFile._parse_definition_message = patched_parse_definition_message

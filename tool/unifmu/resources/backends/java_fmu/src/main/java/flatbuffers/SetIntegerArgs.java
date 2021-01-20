// automatically generated by the FlatBuffers compiler, do not modify

package flatbuffers;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class SetIntegerArgs extends Table {
  public static void ValidateVersion() { Constants.FLATBUFFERS_1_12_0(); }
  public static SetIntegerArgs getRootAsSetIntegerArgs(ByteBuffer _bb) { return getRootAsSetIntegerArgs(_bb, new SetIntegerArgs()); }
  public static SetIntegerArgs getRootAsSetIntegerArgs(ByteBuffer _bb, SetIntegerArgs obj) { _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __reset(_i, _bb); }
  public SetIntegerArgs __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public int references(int j) { int o = __offset(4); return o != 0 ? bb.getInt(__vector(o) + j * 4) : 0; }
  public int referencesLength() { int o = __offset(4); return o != 0 ? __vector_len(o) : 0; }
  public IntVector referencesVector() { return referencesVector(new IntVector()); }
  public IntVector referencesVector(IntVector obj) { int o = __offset(4); return o != 0 ? obj.__assign(__vector(o), bb) : null; }
  public ByteBuffer referencesAsByteBuffer() { return __vector_as_bytebuffer(4, 4); }
  public ByteBuffer referencesInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 4, 4); }
  public int values(int j) { int o = __offset(6); return o != 0 ? bb.getInt(__vector(o) + j * 4) : 0; }
  public int valuesLength() { int o = __offset(6); return o != 0 ? __vector_len(o) : 0; }
  public IntVector valuesVector() { return valuesVector(new IntVector()); }
  public IntVector valuesVector(IntVector obj) { int o = __offset(6); return o != 0 ? obj.__assign(__vector(o), bb) : null; }
  public ByteBuffer valuesAsByteBuffer() { return __vector_as_bytebuffer(6, 4); }
  public ByteBuffer valuesInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 6, 4); }

  public static int createSetIntegerArgs(FlatBufferBuilder builder,
      int referencesOffset,
      int valuesOffset) {
    builder.startTable(2);
    SetIntegerArgs.addValues(builder, valuesOffset);
    SetIntegerArgs.addReferences(builder, referencesOffset);
    return SetIntegerArgs.endSetIntegerArgs(builder);
  }

  public static void startSetIntegerArgs(FlatBufferBuilder builder) { builder.startTable(2); }
  public static void addReferences(FlatBufferBuilder builder, int referencesOffset) { builder.addOffset(0, referencesOffset, 0); }
  public static int createReferencesVector(FlatBufferBuilder builder, int[] data) { builder.startVector(4, data.length, 4); for (int i = data.length - 1; i >= 0; i--) builder.addInt(data[i]); return builder.endVector(); }
  public static void startReferencesVector(FlatBufferBuilder builder, int numElems) { builder.startVector(4, numElems, 4); }
  public static void addValues(FlatBufferBuilder builder, int valuesOffset) { builder.addOffset(1, valuesOffset, 0); }
  public static int createValuesVector(FlatBufferBuilder builder, int[] data) { builder.startVector(4, data.length, 4); for (int i = data.length - 1; i >= 0; i--) builder.addInt(data[i]); return builder.endVector(); }
  public static void startValuesVector(FlatBufferBuilder builder, int numElems) { builder.startVector(4, numElems, 4); }
  public static int endSetIntegerArgs(FlatBufferBuilder builder) {
    int o = builder.endTable();
    builder.required(o, 4);  // references
    builder.required(o, 6);  // values
    return o;
  }

  public static final class Vector extends BaseVector {
    public Vector __assign(int _vector, int _element_size, ByteBuffer _bb) { __reset(_vector, _element_size, _bb); return this; }

    public SetIntegerArgs get(int j) { return get(new SetIntegerArgs(), j); }
    public SetIntegerArgs get(SetIntegerArgs obj, int j) {  return obj.__assign(__indirect(__element(j), bb), bb); }
  }
}

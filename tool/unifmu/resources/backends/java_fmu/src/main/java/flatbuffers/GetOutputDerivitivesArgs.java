// automatically generated by the FlatBuffers compiler, do not modify

package flatbuffers;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class GetOutputDerivitivesArgs extends Table {
  public static void ValidateVersion() { Constants.FLATBUFFERS_1_12_0(); }
  public static GetOutputDerivitivesArgs getRootAsGetOutputDerivitivesArgs(ByteBuffer _bb) { return getRootAsGetOutputDerivitivesArgs(_bb, new GetOutputDerivitivesArgs()); }
  public static GetOutputDerivitivesArgs getRootAsGetOutputDerivitivesArgs(ByteBuffer _bb, GetOutputDerivitivesArgs obj) { _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __reset(_i, _bb); }
  public GetOutputDerivitivesArgs __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }


  public static void startGetOutputDerivitivesArgs(FlatBufferBuilder builder) { builder.startTable(0); }
  public static int endGetOutputDerivitivesArgs(FlatBufferBuilder builder) {
    int o = builder.endTable();
    return o;
  }

  public static final class Vector extends BaseVector {
    public Vector __assign(int _vector, int _element_size, ByteBuffer _bb) { __reset(_vector, _element_size, _bb); return this; }

    public GetOutputDerivitivesArgs get(int j) { return get(new GetOutputDerivitivesArgs(), j); }
    public GetOutputDerivitivesArgs get(GetOutputDerivitivesArgs obj, int j) {  return obj.__assign(__indirect(__element(j), bb), bb); }
  }
}

// automatically generated by the FlatBuffers compiler, do not modify

package flatbuffers;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class DoStepArgs extends Table {
  public static void ValidateVersion() { Constants.FLATBUFFERS_1_12_0(); }
  public static DoStepArgs getRootAsDoStepArgs(ByteBuffer _bb) { return getRootAsDoStepArgs(_bb, new DoStepArgs()); }
  public static DoStepArgs getRootAsDoStepArgs(ByteBuffer _bb, DoStepArgs obj) { _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __reset(_i, _bb); }
  public DoStepArgs __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public double currentTime() { int o = __offset(4); return o != 0 ? bb.getDouble(o + bb_pos) : 0.0; }
  public double stepSize() { int o = __offset(6); return o != 0 ? bb.getDouble(o + bb_pos) : 0.0; }
  public boolean noStepPrior() { int o = __offset(8); return o != 0 ? 0!=bb.get(o + bb_pos) : false; }

  public static int createDoStepArgs(FlatBufferBuilder builder,
      double current_time,
      double step_size,
      boolean no_step_prior) {
    builder.startTable(3);
    DoStepArgs.addStepSize(builder, step_size);
    DoStepArgs.addCurrentTime(builder, current_time);
    DoStepArgs.addNoStepPrior(builder, no_step_prior);
    return DoStepArgs.endDoStepArgs(builder);
  }

  public static void startDoStepArgs(FlatBufferBuilder builder) { builder.startTable(3); }
  public static void addCurrentTime(FlatBufferBuilder builder, double currentTime) { builder.addDouble(0, currentTime, 0.0); }
  public static void addStepSize(FlatBufferBuilder builder, double stepSize) { builder.addDouble(1, stepSize, 0.0); }
  public static void addNoStepPrior(FlatBufferBuilder builder, boolean noStepPrior) { builder.addBoolean(2, noStepPrior, false); }
  public static int endDoStepArgs(FlatBufferBuilder builder) {
    int o = builder.endTable();
    return o;
  }

  public static final class Vector extends BaseVector {
    public Vector __assign(int _vector, int _element_size, ByteBuffer _bb) { __reset(_vector, _element_size, _bb); return this; }

    public DoStepArgs get(int j) { return get(new DoStepArgs(), j); }
    public DoStepArgs get(DoStepArgs obj, int j) {  return obj.__assign(__indirect(__element(j), bb), bb); }
  }
}
